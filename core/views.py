import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CodingChallenge, SelectedChallenge
from .serializers import RegisterSerializer, SelectedChallengeSerializer


def clean_stderr(stderr: str) -> str:
    if not stderr or 'SyntaxError' in stderr:
        return stderr
    lines = stderr.strip().split('\n')
    for line in reversed(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('File ') and not stripped.startswith('Traceback'):
            return stripped
    return stderr


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        all_challenges = list(CodingChallenge.objects.all())
        if len(all_challenges) < 3:
            return Response(
                {'detail': 'Not enough challenges in the database. Run seed_challenges first.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        chosen = random.sample(all_challenges, 3)
        selected = []
        for challenge in chosen:
            selected.append(SelectedChallenge(
                applicant=user,
                challenge=challenge,
                submission=challenge.init_temp,
            ))
        SelectedChallenge.objects.bulk_create(selected)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class ChallengeListView(APIView):
    def get(self, request):
        # select_related avoids N+1 queries when serializing nested challenge data
        selected = (
            SelectedChallenge.objects
            .filter(applicant=request.user)
            .select_related('challenge')
            .order_by('challenge__order')
        )
        serializer = SelectedChallengeSerializer(selected, many=True)
        return Response(serializer.data)


class SaveSubmissionView(APIView):
    # NOTE: This view intentionally does NOT import or call judge0.py
    def patch(self, request, pk):
        selected = get_object_or_404(
            SelectedChallenge, pk=pk, applicant=request.user
        )
        submission = request.data.get('submission', '')
        selected.submission = submission
        selected.save(update_fields=['submission'])
        return Response({'status': 'saved'})


class RunCodeView(APIView):
    def post(self, request, pk):
        from . import judge0  # local import enforces Judge0-only-in-run-view rule

        selected = get_object_or_404(
            SelectedChallenge, pk=pk, applicant=request.user
        )

        user_code = request.data.get('submission', selected.submission)
        if not user_code or not user_code.strip():
            return Response(
                {'detail': 'No code submitted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save latest submission regardless of pass/fail
        selected.submission = user_code
        selected.save(update_fields=['submission'])

        try:
            source = judge0.build_source(user_code, selected.challenge.tests)
            token = judge0.submit_to_judge0(source)
            result = judge0.poll_result(token)
        except TimeoutError:
            return Response(
                {'detail': 'Code execution timed out. Please try again.'},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except ConnectionError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Only mark passed=True, never revert to False once passed
        if result['passed'] and not selected.passed:
            selected.passed = True
            selected.save(update_fields=['passed'])

        return Response({
            'passed': selected.passed,
            'stdout': result['stdout'],
            'stderr': clean_stderr(result['stderr']),
        })


class UserCompleteView(APIView):
    def patch(self, request):
        user = request.user
        selected = SelectedChallenge.objects.filter(applicant=user)

        if selected.count() < 3:
            return Response(
                {'detail': 'Challenges not yet assigned.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if selected.filter(passed=False).exists():
            return Response(
                {'detail': 'All challenges must be passed before submitting.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.completed = True
        user.save(update_fields=['completed'])
        return Response({'detail': 'Application submitted successfully.'})

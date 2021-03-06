"""
Serializers that can be shared across multiple versions of the API
should be created here. As the API evolves, serializers may become more
specific to a particular version of the API. In this case, the serializers
in question should be moved to versioned sub-package.
"""
from rest_framework import serializers
from user_tasks.models import UserTaskStatus

from registrar.apps.core.proxies import DiscoveryProgram
from registrar.apps.core.utils import get_effective_user_program_api_permissions
from registrar.apps.enrollments.constants import (
    COURSE_ENROLLMENT_STATUSES,
    PROGRAM_ENROLLMENT_STATUSES,
)


# pylint: disable=abstract-method
class DiscoveryProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for DiscoveryPrograms.
    """
    program_key = serializers.CharField(source='key')
    program_title = serializers.CharField(source='title')
    program_url = serializers.URLField(source='url')
    permissions = serializers.SerializerMethodField(source='get_permissions')

    class Meta:
        model = DiscoveryProgram
        fields = (
            'program_key',
            'program_title',
            'program_url',
            'program_type',
            'permissions',
        )

    def get_permissions(self, program):
        """
        Get list of permissions granted to user making the request from the context
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user_permissions = get_effective_user_program_api_permissions(request.user, program)

            return sorted(permission.name for permission in user_permissions)
        else:
            return []


class ProgramEnrollmentRequestSerializer(serializers.Serializer):
    """
    Serializer for request to create a program enrollment
    """
    student_key = serializers.CharField()
    status = serializers.ChoiceField(choices=PROGRAM_ENROLLMENT_STATUSES)


class ProgramEnrollmentModificationRequestSerializer(serializers.Serializer):
    """
    Serializer for request to modify a program enrollment
    """
    student_key = serializers.CharField()
    status = serializers.ChoiceField(choices=PROGRAM_ENROLLMENT_STATUSES)


class CourseEnrollmentRequestSerializer(serializers.Serializer):
    """
    Serializer for a request to create a course enrollment
    """
    student_key = serializers.CharField()
    status = serializers.ChoiceField(choices=COURSE_ENROLLMENT_STATUSES)


class CourseEnrollmentModificationRequestSerializer(serializers.Serializer):
    """
    Serializer for a request to modify a course enrollment
    """
    student_key = serializers.CharField()
    status = serializers.ChoiceField(choices=COURSE_ENROLLMENT_STATUSES)


class CourseRunSerializer(serializers.Serializer):
    """
    Serializer for a course run returned from the
    Course Discovery Service
    """
    course_id = serializers.CharField(source='key')
    external_course_key = serializers.CharField(source='external_key')
    course_title = serializers.CharField(source='title')
    course_url = serializers.URLField(source='marketing_url')


class JobAcceptanceSerializer(serializers.Serializer):
    """
    Serializer for data about the invocation of a job.
    """
    job_id = serializers.UUIDField()
    job_url = serializers.URLField()


class JobStatusSerializer(serializers.Serializer):
    """
    Serializer for data about the status of a job.
    """
    STATUS_CHOICES = {
        UserTaskStatus.PENDING,
        UserTaskStatus.IN_PROGRESS,
        UserTaskStatus.SUCCEEDED,
        UserTaskStatus.FAILED,
        UserTaskStatus.RETRYING,
    }

    job_id = serializers.UUIDField()
    name = serializers.CharField(allow_null=False)
    created = serializers.DateTimeField()
    state = serializers.ChoiceField(choices=STATUS_CHOICES)
    result = serializers.URLField(allow_null=True)
    text = serializers.CharField(allow_null=True)


class ProgramReportMetadataSerializer(serializers.Serializer):
    """
    Serializer for metadata about a program report.
    """
    name = serializers.CharField()
    created_date = serializers.DateField()
    download_url = serializers.URLField()

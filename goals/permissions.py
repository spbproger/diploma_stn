from rest_framework import permissions
from goals.models import BoardParticipant, Goal, GoalCategory, Board, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalCategory):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Goal):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalComment):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.goal.category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()

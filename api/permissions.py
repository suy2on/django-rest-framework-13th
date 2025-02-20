from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(obj)
        print(request.user)
        if request.method in permissions.SAFE_METHODS:
            print(obj)
            print(request.user)
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author.user == request.user    # obj.author -> Profile / profile.user -> User
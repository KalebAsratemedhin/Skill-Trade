
from backend.users.models import User


class UserService:
    def get_all_users(self):
        return User.objects.all()
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
    def create_user(self, data):
        return User.objects.create_user(**data)
    def update_user(self, user, data):
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()
        return user
    def delete_user(self, user):
        user.delete()
        return user
    
    
class TechnicianService(UserService):
    def get_technicians(self):
        return User.objects.filter(role="technician")
    def get_technician(self, technician_id):
        return User.objects.get(id=technician_id, role="technician")
    def create_technician(self, data):
        return User.objects.create_user(role="technician", **data)
    def update_technician(self, technician, data):
        return super().update_user(technician, data)


def profile_serializer(profile):
    return {
        'id': profile.user.id,
        'name': profile.name,
        # 'email': profile.email,
        # 'first_name': profile.first_name,
        # 'last_name': profile.last_name,
        # 'is_staff': profile.is_staff,
        # 'is_active': profile.is_active,
        'age': profile.age,
        'gender': profile.gender,
        'date_joined': profile.user.date_joined,
        'last_login': profile.user.last_login,
    }
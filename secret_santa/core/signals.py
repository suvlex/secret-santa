def change_member(sender, instance, **kwargs):
    member = instance.member
    member.hashed_member_info = member.get_hashed_member_info()
    member.save()

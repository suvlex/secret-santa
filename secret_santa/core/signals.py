def change_member(sender, instance, **kwargs):
    member = instance.member
    member.hashed_email = member.get_hashed_email()
    member.save()

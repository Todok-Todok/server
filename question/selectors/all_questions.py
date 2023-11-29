# <SELECT, EXISTS 쿼리만을 수행하는 Selector 예시>

# def get_post_by_id(post_id: int) -> Optional[Post]:
#     try:
# 	return Post.objects.filter(id=post_id, deleted_at__isnull=True).get()
#     except Post.DoesNotExist:
# 	return None

# def get_post_queryset_by_user_id(user_id: int) -> "QuerySet[Post]":
#     return Post.objects.filter(user_id=user_id, deleted_at__isnull=True)

# def check_is_exists_post_by_user_id(user_id: int) -> bool:
#     return Post.objects.filter(user_id=user_id, deleted_at__isnull=True).exists()
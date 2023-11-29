# <데이터 검증의 역할이 분리된 Validator 레이어 예시>
# import pydantic
# class PostCreateValidator(pydantic.Basemodel):
#     title: str
#     text: str

#     @validator("title")
#     def title_length(cls, v):
#         if len(title) > 100:
#             raise ValueError("Post title must be 100 characters or less.")

#     @validator("text")
#     def text_length(cls, v):
#         if len(text) > 1000:
#             raise ValueError("Post text must be 1000 characters or less.")
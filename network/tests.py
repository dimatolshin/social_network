# def fibo2(n: int):
#     if n <= 1:
#         return n
#     return fibo2(n - 1) + fibo2(n - 2)
#
#
# for i in range(10):
#     print(f'{i}:{fibo2(i)}')


# def fibo1(n):
#     if n <= 1:
#         return n
#     nums = [0]*(n+1)
#     nums[1] = 1
#     for i in range(2, n+1):
#         nums[i] = nums[i-1]+nums[i-2]
#     return nums[n]
#
#
# print(fibo1(100))


# def stone(n: list) -> list:
#     for _ in range(len(n)):
#         for i in range(0, len(n) - 1):
#             if n[i] > n[i + 1]:
#                 n[i], n[i + 1] = n[i + 1], n[i]
#     return n
#
#
# print(stone([3, 2, 1, 7, 10, 9]))


# def input(a:list):
#     n=len(a)
#     for _ in range(n):
#         for i in range(1,n-1):
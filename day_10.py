def look_and_say(input):
    say = []
    cnt = 0
    cur = input[0]
    for x in input:
        if x == cur:
            cnt += 1
        else:
            say.append(str(cnt) + cur)
            cnt = 1
            cur = x
    say.append(str(cnt) + cur)
    say = ''.join(say)
    print('look_and_say', input, '->', say)
    # print('look', input)
    # print('say', say)
    return say

# input = '1'
input = '1113122113'
repeat = 50
for i in range(repeat):
    input = look_and_say(input)
    print(len(input))

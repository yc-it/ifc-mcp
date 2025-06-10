def success(data=None, msg='成功'):
    return res(code=200, msg=msg, data=data)

def fail(data=None, msg='失败'):
    return res(code=400, msg=msg, data=data)

def res(code=400, msg='错误', data=None):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }
from appdir import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 调试模式
    # app.run() # 生产模式

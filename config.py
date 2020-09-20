
class Settings():
    app_name: str = "Line_todo"
    admin_email: str = ""

    bot_name: str = "サボり君"

    channel_secret: str = ""
    channel_access_token: str = ""

    db_path: str = "sqlite:///line_todo.sqlite3"
    log_file_path: str = "logfile/logger.log"
    
class Messages():
    # reply message
    Invalid_formard = "無効なフォマードです。\n■フォーマット:\nサボり君,\n■担当者,\n■タスク期限,\n■タスク内容,\n■依頼者\n※注意:\nカンマ区切り必須\nタスク期限は未来時刻"
    Accepted = "('◇')ゞラジャー！"
    Task_done = '■タスク期限になりました\n%s\n■担当者:\n%s\n■タスク内容:\n%s\n■依頼者:\n%s\n'
"""
一鍵取得所有 API 憑證 — 只需要照步驟操作，不需要任何技術知識。
執行：python setup_credentials.py
"""
import webbrowser
import time
import os
import shutil

def write_env(claude_key, threads_token, threads_user_id):
    content = f"""# AI 選股機器人 API Keys
CLAUDE_API_KEY={claude_key}
THREADS_ACCESS_TOKEN={threads_token}
THREADS_USER_ID={threads_user_id}
"""
    with open(".env", "w", encoding="utf-8") as f:
        f.write(content)
    print("\n✅ .env 檔案已建立成功！")

def step_claude():
    print("\n" + "="*55)
    print("【步驟 1/3】取得 Claude API Key")
    print("="*55)
    print("即將開啟瀏覽器 → console.anthropic.com")
    print()
    print("到了網站後：")
    print("  1. 用 Google 帳號登入")
    print("  2. 左側點「API Keys」")
    print("  3. 點「+ Create Key」")
    print("  4. Key 名稱隨便取（如：threads-bot）")
    print("  5. 複製 sk-ant-... 開頭的 Key")
    print()
    input("按 Enter 開啟瀏覽器...")
    webbrowser.open("https://console.anthropic.com/settings/keys")
    print("\n（瀏覽器已開啟，完成後回來這裡）")
    key = input("貼上你的 Claude API Key：").strip()
    return key

def step_threads_app():
    print("\n" + "="*55)
    print("【步驟 2/3】建立 Threads API App")
    print("="*55)
    print("即將開啟瀏覽器 → Meta for Developers")
    print()
    print("到了網站後：")
    print("  1. 點右上角「My Apps」→「Create App」")
    print("  2. 選「Other」→「Next」")
    print("  3. 選「Consumer」→「Next」")
    print("  4. App 名稱：threads-stock-bot")
    print("  5. 建立完成後，左側找「Threads API」→ 點「Set Up」")
    print()
    input("按 Enter 開啟瀏覽器...")
    webbrowser.open("https://developers.facebook.com/apps/")
    print("\n（瀏覽器已開啟，完成建立 App 後回來這裡）")
    input("App 建立完成後按 Enter 繼續...")

def step_threads_token():
    print("\n" + "="*55)
    print("【步驟 3/3】取得 Threads Access Token")
    print("="*55)
    print("現在需要在剛才建立的 App 裡取得 Token")
    print()
    print("操作步驟：")
    print("  1. 在 App 頁面左側點「Threads API」")
    print("  2. 找到「Generate token」區塊")
    print("  3. 點你的 Threads 帳號授權")
    print("  4. 複製顯示的 Access Token（很長的一串）")
    print("  5. 同頁面找到「Threads User ID」（純數字）")
    print()
    input("按 Enter 繼續（不需要再開瀏覽器，剛才那個頁面還在）...")
    token = input("\n貼上 Access Token：").strip()
    user_id = input("貼上 User ID（純數字）：").strip()
    return token, user_id

def main():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║    AI 選股機器人  憑證設定精靈        ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print("這個程式會引導你取得所有需要的 API Key。")
    print("總共 3 個步驟，預計 10-15 分鐘。")
    print()
    input("準備好了嗎？按 Enter 開始...")

    # Step 1: Claude
    claude_key = step_claude()
    if not claude_key.startswith("sk-"):
        print("⚠️  Key 格式看起來不對，請確認是否完整複製")

    # Step 2: Create Threads App
    step_threads_app()

    # Step 3: Get Threads Token
    threads_token, threads_user_id = step_threads_token()

    # Write .env
    print("\n" + "="*55)
    print("正在建立設定檔...")
    write_env(claude_key, threads_token, threads_user_id)

    # Test
    print("\n要立刻測試連線嗎？")
    choice = input("輸入 y 測試，直接 Enter 跳過：").strip().lower()
    if choice == 'y':
        os.system(f'"{__import__("sys").executable}" test_connection.py')

    print("\n" + "="*55)
    print("✅ 設定完成！")
    print()
    print("現在可以執行：")
    print("  → 雙擊 start_bot.bat  啟動機器人")
    print("  → 機器人會在 週一/三/五 晚上 8 點自動發文")
    print("  → 每 2 小時自動回覆留言")
    print("="*55)

if __name__ == "__main__":
    main()

cat << 'EOF' > agent_code/test_agent.py
import requests
import psycopg2
import os

# Test Ollama / Gemma connection
def test_llm():
    print("Testing connection to Gemma (Ollama)...")
    try:
        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "gemma:7b",
                "prompt": "Say hello in one short sentence.",
                "stream": False
            }
        )
        if response.status_code == 200:
            print("✅ LLM Success! Response:", response.json().get("response", "").strip())
        else:
            print("❌ LLM Error:", response.text)
    except Exception as e:
        print("❌ LLM Connection Failed:", e)

# Test PostgreSQL connection
def test_db():
    print("Testing connection to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname="agent_memory",
            user="gemma_user",
            password="secure_password",
            host="agent_db",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"✅ Database Success! Connected to: {db_version[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Database Connection Failed:", e)

if __name__ == "__main__":
    test_llm()
    test_db()
EOF
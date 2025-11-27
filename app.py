import base64
import streamlit as st
import traceback

# ---------------- AXM Cipher Core Functions ---------------- #

def axm_generate_matrix(key):
    """Generate numeric matrix using ASCII of key"""
    return [(ord(c) % 9) + 3 for c in key]  # values: 3–11

def axm_encrypt(text, key):
    if not key:
        return ""
    matrix = axm_generate_matrix(key)
    encrypted_values = []

    for i, ch in enumerate(text):
        step1 = ord(ch) * matrix[i % len(matrix)]        # ASCII × MATRIX
        step2 = step1 ^ ord(key[i % len(key)])           # XOR with key
        encrypted_values.append(str(step2))

    encrypted_string = ",".join(encrypted_values)
    return base64.b64encode(encrypted_string.encode()).decode()  # base64

def axm_decrypt(cipher, key):
    if not key:
        return ""
    try:
        matrix = axm_generate_matrix(key)
        values = base64.b64decode(cipher).decode().split(",")
        result = ""

        for i, val in enumerate(values):
            step1 = int(val) ^ ord(key[i % len(key)])        # reverse XOR
            step2 = step1 // matrix[i % len(matrix)]         # divide back matrix
            result += chr(step2)

        return result
    except Exception as e:
        # return the error message for debugging
        return f"❌ Decryption Failed — invalid cipher text or key.\n\nError: {e}"

# -------------------- Streamlit Web UI -------------------- #

st.set_page_config(page_title="AXM Cipher", page_icon="🛡", layout="centered")
st.title("🛡 AXM Cipher – ASCII × Matrix XOR Method")
st.write("A proprietary encryption system designed for project use. 🔐")

mode = st.radio("Select Mode", ["Encrypt", "Decrypt"], horizontal=True)

text_input_label = "Enter plain text to encrypt" if mode == "Encrypt" else "Enter AXM cipher text to decrypt"
text = st.text_area(text_input_label, height=180, key="text_area")

key = st.text_input("Enter secret key", type="password", key="secret_key")

# initialize session state storage for output
if "axm_output" not in st.session_state:
    st.session_state.axm_output = ""

# Use a form or a button; form avoids double-run issues sometimes
with st.form("axm_form"):
    submit = st.form_submit_button("Run")

if submit:
    try:
        if not text:
            st.warning("⚠ Please enter text.")
        elif not key:
            st.warning("⚠ Key cannot be empty.")
        else:
            if mode == "Encrypt":
                st.session_state.axm_output = axm_encrypt(text, key)
            else:
                st.session_state.axm_output = axm_decrypt(text, key)
    except Exception:
        # show stack trace in console and a short message in UI
        st.error("An unexpected error occurred. Check your console for details.")
        print("Traceback (from streamlit):")
        traceback.print_exc()

# display output if present
if st.session_state.axm_output:
    st.subheader("🔽 Output")
    st.code(st.session_state.axm_output)

    if mode == "Encrypt":
        st.download_button(
            label="💾 Download Cipher as .txt",
            data=st.session_state.axm_output,
            file_name="axm_cipher.txt",
            mime="text/plain"
        )

st.markdown("---")
st.caption("🔐 Powered by AXM (ASCII × Matrix XOR Method) — Developed for Academic/Research Use")

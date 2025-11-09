import re
import streamlit as st

def truncate_email_content(email_content, max_tokens=5000):
    """
    Truncate email content to fit within token limits.
    
    Args:
        email_content (str): The original email content
        max_tokens (int): Maximum tokens allowed (approx 4 chars per token)
    
    Returns:
        str: Truncated email content
    """
    # Simple character-based truncation (approx 4 chars per token)
    max_chars = max_tokens * 4
    if len(email_content) > max_chars:
        truncated = email_content[:max_chars] + "... [content truncated]"
        st.warning(f"📝 Email was truncated from {len(email_content)} to {max_chars} characters for processing.")
        return truncated
    return email_content

def clean_email_content(email_content):
    """
    Remove unnecessary parts from email to reduce token count.
    
    Args:
        email_content (str): The original email content
    
    Returns:
        str: Cleaned email content
    """
    # Remove long quoted/reply sections
    lines = email_content.split('\n')
    cleaned_lines = []
    in_quoted_section = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip quoted/reply sections
        if line_stripped.startswith(('>', 'On', 'From:', 'Sent:', 'To:', 'Subject:')):
            if not in_quoted_section:
                in_quoted_section = True
            continue
        elif in_quoted_section and line_stripped == '':
            in_quoted_section = False
            continue
        
        if not in_quoted_section:
            cleaned_lines.append(line)
    
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Remove multiple consecutive newlines
    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
    
    # Remove extra whitespace
    cleaned_content = re.sub(r'[ \t]+', ' ', cleaned_content)
    
    return cleaned_content.strip()

def preprocess_email(email_content, max_tokens=5000):
    """
    Main preprocessing function: clean and truncate email content.
    
    Args:
        email_content (str): Original email content
        max_tokens (int): Token limit for processing
    
    Returns:
        str: Processed email content ready for AI analysis
    """
    # Step 1: Clean the email
    cleaned_content = clean_email_content(email_content)
    
    # Step 2: Truncate if necessary
    processed_content = truncate_email_content(cleaned_content, max_tokens)
    
    return processed_content

def split_email_content(email_content, max_chunk_size=4000):
    """
    Split email content into manageable chunks for very long emails.
    
    Args:
        email_content (str): Email content to split
        max_chunk_size (int): Maximum characters per chunk
    
    Returns:
        list: List of email chunks
    """
    paragraphs = email_content.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
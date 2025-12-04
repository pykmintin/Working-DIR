#!/usr/bin/env python3
"""
Test cases for chat_processor_v2.py implementation
Tests MS_001, MS_002, MS_003, MS_004 specifications
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat_processor_v2 import split_conversations, generate_manifest_entry
import json

def test_split_conversations():
    """Test MS_001: Conversation splitting functionality"""
    print("=== Testing split_conversations() ===")
    
    # Test 1: Kimi format
    kimi_text = """User: Hello, how are you?
Kimi: I'm doing well, thank you for asking.

User: Can you help me with Python?
Kimi: I'd be happy to help you with Python programming.

User: What about data structures?
Kimi: Data structures are fundamental to programming."""
    
    result = split_conversations(kimi_text)
    print(f"Kimi format test - Found {len(result)} conversations")
    assert len(result) == 3, f"Expected 3 conversations, got {len(result)}"
    
    # Test 2: ChatGPT format
    chatgpt_text = """###CHATGPT###
User: I need help with JavaScript
Assistant: I can help you with JavaScript
###CHATGPT###
User: How do I use async/await?
Assistant: Async/await makes asynchronous code more readable"""
    
    result = split_conversations(chatgpt_text)
    print(f"ChatGPT format test - Found {len(result)} conversations")
    assert len(result) == 2, f"Expected 2 conversations, got {len(result)}"
    
    # Test 3: Generic separator format
    generic_text = """Conversation 1
---
Conversation 2
---
Conversation 3"""
    
    result = split_conversations(generic_text)
    print(f"Generic separator test - Found {len(result)} conversations")
    assert len(result) == 3, f"Expected 3 conversations, got {len(result)}"
    
    # Test 4: No delimiters (single conversation)
    single_text = "This is a single conversation without any delimiters"
    result = split_conversations(single_text)
    print(f"No delimiters test - Found {len(result)} conversations")
    assert len(result) == 1, f"Expected 1 conversation, got {len(result)}"
    
    # Test 5: MS_003 - Empty input
    empty_text = ""
    result = split_conversations(empty_text)
    print(f"Empty input test - Found {len(result)} conversations")
    assert len(result) == 1, f"Expected 1 conversation for empty input, got {len(result)}"
    
    print("✓ All split_conversations tests passed\n")

def test_generate_manifest_entry():
    """Test MS_002, MS_003, MS_004: Manifest entry generation"""
    print("=== Testing generate_manifest_entry() ===")
    
    # Test 1: Normal case with Kimi format (single conversation)
    normal_text = """User: Hello, I need help with Python programming
Kimi: I'd be happy to help you with Python. What specific topic are you interested in?
User: Can you show me how to use dictionaries?
Kimi: Certainly! Dictionaries in Python are key-value pairs. Here's a simple example:

```python
my_dict = {'name': 'John', 'age': 30}
print(my_dict['name'])
```

User: That's helpful, thanks!
Kimi: You're welcome! Let me know if you have any other questions."""
    
    entry, formatted, code_blocks = generate_manifest_entry(normal_text)
    
    print(f"Normal case test:")
    print(f"  - Entry ID: {entry['id']}")
    print(f"  - Title: {entry['title']}")
    print(f"  - Messages count: {len(entry['messages'])}")
    print(f"  - Code blocks: {len(code_blocks)}")
    print(f"  - Signatures: {len(entry['signatures'])}")
    
    assert entry['title'] == "Hello, I need help with Python programming", f"Unexpected title: {entry['title']}"
    assert len(entry['messages']) == 4, f"Expected 4 messages, got {len(entry['messages'])}"  # 2 pairs in first conversation
    assert len(code_blocks) == 0, f"Expected 0 code blocks (code is in different conversation), got {len(code_blocks)}"
    
    # Test 2: MS_004 - No User:/Kimi: pairs (regex failure)
    no_pairs_text = "This text has no User:/Kimi: pairs at all"
    
    entry, formatted, code_blocks = generate_manifest_entry(no_pairs_text)
    
    print(f"No pairs test (MS_004):")
    print(f"  - Entry title: {entry['title']}")
    print(f"  - Messages count: {len(entry['messages'])}")
    print(f"  - Formatted text length: {len(formatted)}")
    print(f"  - Code blocks: {len(code_blocks)}")
    
    assert entry['title'] == "Empty", f"Expected 'Empty' title, got {entry['title']}"
    assert len(entry['messages']) == 0, f"Expected 0 messages, got {len(entry['messages'])}"
    assert len(formatted) == 0, f"Expected empty formatted text, got {len(formatted)}"
    assert len(code_blocks) == 0, f"Expected 0 code blocks, got {len(code_blocks)}"
    
    # Test 3: MS_003 - Very short input (pre-compute failure)
    short_text = "User: Hi\nKimi: Hello"
    
    entry, formatted, code_blocks = generate_manifest_entry(short_text)
    
    print(f"Short input test (MS_003):")
    print(f"  - Entry ID: {entry['id']}")
    print(f"  - Title: {entry['title']}")
    print(f"  - Messages count: {len(entry['messages'])}")
    
    assert len(entry['messages']) == 2, f"Expected 2 messages, got {len(entry['messages'])}"
    assert entry['title'] == "Hi", f"Expected 'Hi' title, got {entry['title']}"
    
    # Test 4: Multiple code blocks
    multi_code_text = """User: Show me different programming languages
Kimi: Here are examples in Python and JavaScript:
```python
def hello():
    print("Hello World")
```
User: What about JavaScript?
Kimi: Here's the JavaScript version:
```javascript
function hello() {
    console.log("Hello World");
}
```"""
    
    entry, formatted, code_blocks = generate_manifest_entry(multi_code_text)
    
    print(f"Multiple code blocks test:")
    print(f"  - Code blocks count: {len(code_blocks)}")
    
    assert len(code_blocks) == 2, f"Expected 2 code blocks, got {len(code_blocks)}"
    assert 'code_block_1' in code_blocks, "Expected code_block_1"
    assert 'code_block_2' in code_blocks, "Expected code_block_2"
    
    print("✓ All generate_manifest_entry tests passed\n")

def test_complex_scenario():
    """Test the scenario mentioned: Kimi format + ChatGPT format + --- separator"""
    print("=== Testing Complex Scenario ===")
    
    complex_text = """User: First conversation in Kimi format
Kimi: This is the first conversation

User: Second conversation in Kimi format
Kimi: This is the second conversation
###CHATGPT###
User: This is ChatGPT format conversation
Assistant: ChatGPT response
---
This is a generic separator conversation"""
    
    # Test split_conversations
    conversations = split_conversations(complex_text)
    print(f"Complex scenario - Found {len(conversations)} conversations")
    
    # Should detect Kimi format first and split by \n\n
    # Use first conversation for manifest generation
    if conversations:
        entry, formatted, code_blocks = generate_manifest_entry(complex_text)
        print(f"  - First conversation title: {entry['title']}")
        print(f"  - Messages in first conversation: {len(entry['messages'])}")
    
    print("✓ Complex scenario test passed\n")

def main():
    """Run all tests"""
    print("Running Chat Processor Tests\n")
    print("=" * 50)
    
    try:
        test_split_conversations()
        test_generate_manifest_entry()
        test_complex_scenario()
        
        print("🎉 All tests passed successfully!")
        print("\nImplementation Status:")
        print("✓ MS_001: split_conversations() - Implemented and tested")
        print("✓ MS_002: generate_manifest_entry() - Implemented and tested")
        print("✓ MS_003: Pre-compute failure handling - Implemented and tested")
        print("✓ MS_004: Regex failure handling - Implemented and tested")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
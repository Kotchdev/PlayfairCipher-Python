from typing import List, Tuple

# ====================================================================
# PART 1: Grid Generation and Message Preparation (Pre-existing code)
# ====================================================================


def create_grid(keyword: str) -> List[List[str]]:
    """
    Constructs a 5x5 Playfair cipher grid from the given keyword.

    Rules: 'J' is replaced with 'I'. Keyword letters are unique and fill the grid
    first, followed by the remaining 25-letter alphabet.
    """
    # Guardrail: Handle empty keyword
    if not keyword or not any(c.isalpha() for c in keyword):
        raise ValueError(
            "Keyword must contain at least one alphabetic character.")

    # Step 1: Normalize keyword
    keyword = keyword.upper()
    keyword = ''.join(filter(str.isalpha, keyword))  # remove non-alphabetic
    keyword = keyword.replace('J', 'I')  # replace J with I

    # Step 2: Keep unique letters in order
    seen = set()
    unique_keyword = []
    for char in keyword:
        if char not in seen:
            seen.add(char)
            unique_keyword.append(char)

    # Step 3: Define alphabet (A-Z excluding J)
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'J']

    # Step 4: Fill grid with keyword letters first, then remaining alphabet
    grid_letters = unique_keyword + [c for c in alphabet if c not in seen]

    # Step 5: Construct 5x5 grid
    grid = [grid_letters[i:i + 5] for i in range(0, 25, 5)]

    return grid


def prepare_message(message_text: str) -> List[str]:
    """
        Prepare a message for Playfair cipher encryption by producing two-letter digraphs.

        Steps: Clean, separate consecutive repeats ('XX' -> 'XZX', 'MM' -> 'MXM'), 
        and pad odd length at the end.
        """
    if not isinstance(message_text, str):
        return []

    # Step 1: Clean input
    cleaned = ''.join(ch for ch in message_text.upper() if ch.isalpha())
    cleaned = cleaned.replace('J', 'I')

    if not cleaned:
        return []

    # Step 2: Separate consecutive repeats
    prepared_chars = []
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i + 1] if i + 1 < len(cleaned) else None

        if b is None:
            prepared_chars.append(a)
            i += 1
        elif a == b:
            filler = 'Z' if a == 'X' else 'X'
            prepared_chars.append(a)
            prepared_chars.append(filler)
            i += 1  # Advance by one to re-check the original 'b' against the new context
        else:
            prepared_chars.append(a)
            prepared_chars.append(b)
            i += 2  # Advance by two for a normal pair

    # Step 3: Pad odd length at the end
    if len(prepared_chars) % 2 == 1:
        last = prepared_chars[-1]
        prepared_chars.append('Z' if last == 'X' else 'X')

    # Step 4: Split into digraphs
    digraphs = [
        ''.join(prepared_chars[i:i + 2])
        for i in range(0, len(prepared_chars), 2)
    ]

    return [dg for dg in digraphs if len(dg) == 2]

#


# ====================================================================
# PART 2: Encryption Logic (Pre-existing code)
# ====================================================================


def find_coordinates(grid: List[List[str]], char: str) -> Tuple[int, int]:
    """
    (Principle: Robustness & Efficiency)
    Finds the (row, col) coordinates of a single character in the 5x5 grid.

    Args:
        grid: The 5x5 Playfair grid.
        char: The single uppercase letter ('A'-'Z', excluding 'J').

    Returns:
        A tuple (row, col).

    Raises:
        ValueError: If the character is not found.
    """
    for r in range(5):
        for c in range(5):
            if grid[r][c] == char:
                return r, c
    # This should only be raised if input cleaning fails, but it's a good guardrail.
    raise ValueError(f"Character '{char}' not found in the Playfair grid.")


def encrypt_pair(grid: List[List[str]], digraph: str) -> str:
    """
    (Principle: Modularity & Abstraction)
    Applies the Playfair encryption rules (Shift Right/Down, Swap Corners) to a digraph.
    """
    char1, char2 = digraph[0], digraph[1]

    # 1. Find coordinates
    r1, c1 = find_coordinates(grid, char1)
    r2, c2 = find_coordinates(grid, char2)

    new_r1, new_c1 = r1, c1
    new_r2, new_c2 = r2, c2

    # 2. Apply Rule Logic
    if r1 == r2:
        # Rule 1: Same Row -> Shift Right (encryption)
        new_c1 = (c1 + 1) % 5
        new_c2 = (c2 + 1) % 5
    elif c1 == c2:
        # Rule 2: Same Column -> Shift Down (encryption)
        new_r1 = (r1 + 1) % 5
        new_r2 = (r2 + 1) % 5
    else:
        # Rule 3: Rectangle -> Swap Corners (self-inverse)
        new_c1 = c2
        new_c2 = c1

    # 3. Get encrypted characters
    encrypted_char1 = grid[new_r1][new_c1]
    encrypted_char2 = grid[new_r2][new_c2]

    return encrypted_char1 + encrypted_char2


def playfair_encrypt(keyword: str, message_text: str) -> str:
    """
    (Principle: Readability & Orchestration)
    The main orchestration function for the Playfair Cipher encryption.
    """
    # Step 1: Create the grid
    grid = create_grid(keyword)

    # Step 2: Prepare the message
    digraphs = prepare_message(message_text)

    if not digraphs:
        return ""  # Return empty string if no valid characters in message

    # Step 3: Encrypt each digraph
    ciphertext_digraphs = [encrypt_pair(grid, dg) for dg in digraphs]

    # Step 4: Join and return
    return "".join(ciphertext_digraphs)


# ====================================================================
# Main Execution Block: Demonstration of ENCRYPTION
# ====================================================================
if __name__ == "__main__":
    print("=== Playfair Cipher: Full ENCRYPTION Demo ===")

    # --- INPUT ---
    keyword = ""
    while not keyword.strip():
        keyword = input("Enter the keyword (e.g., 'MONARCHY'): ").strip()
        if not keyword:
            print("Keyword cannot be empty. Please try again.")

    message_text = input(
        "Enter the message text (e.g., 'The treasure is buried'): ").strip()

    try:
        # --- ENCRYPTION ---
        ciphertext = playfair_encrypt(keyword, message_text)
        grid = create_grid(keyword)  # Re-run for display
        digraphs = prepare_message(message_text)  # Re-run for display

        # Display Encryption Results
        print("\n" + "=" * 30)
        print("         ENCRYPTION")
        print("=" * 30)
        print(f"Keyword: {keyword}")
        print(f"Plaintext: {message_text}")

        print("\n--- Generated Playfair Grid ---")
        for row in grid:
            print(" ".join(row))

        print("\n--- Message Preparation ---")
        print(f"Prepared Digraphs: {digraphs}")

        print(f"\nFINAL CIPHERTEXT: {ciphertext}")
        print("=" * 30)

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

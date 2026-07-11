"""
DecodeLabs Internship - Task 3: RANDOM PASSWORD GENERATOR
--------------------------------------------------------------
Goal: Generate secure random passwords based on user preferences
      (length, and whether to include uppercase, numbers, and
      special characters like @, #, $).

Key Skills:
    - Python's `string` module for character classification
      (letters, digits, punctuation)
    - Python's `secrets` module for CRYPTOGRAPHICALLY SECURE
      randomness (NOT the `random` module - that's predictable
      and unsafe for anything security-related)
    - The Accumulator Pattern again, but this time building up
      a password string character by character instead of a sum

IPO Model:
    Input   -> desired length + which character sets to include
    Process -> build a "pool" of allowed characters, guarantee at
               least one character from each chosen category, then
               fill the rest randomly and shuffle
    Output  -> the generated password printed to the user
"""

import string
import secrets   # cryptographically secure PRNG - the "mandated cryptography"


# -------------------- Character Classification --------------------
# Standardizing character sets using Python's built-in string module,
# instead of hand-typing "abcdefg..." (avoids typos, easy to extend).

LOWERCASE = string.ascii_lowercase          # a-z
UPPERCASE = string.ascii_uppercase          # A-Z
DIGITS = string.digits                      # 0-9
SPECIAL = "@#$%&*!?"                        # curated symbol set (safe subset)


# -------------------- Input / Validation Layer --------------------

def ask_yes_no(prompt):
    """Gatekeeper for yes/no questions - keeps asking until valid input."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(" Please answer with 'y' or 'n'.")


def ask_length():
    """Gatekeeper for password length - must be a sensible integer."""
    while True:
        raw = input("Password length (recommended 12+): ").strip()
        if not raw.isdigit():
            print(" Please enter a whole number.")
            continue
        length = int(raw)
        if length < 4:
            print(" Length must be at least 4 to fit all character types.")
            continue
        return length


# -------------------- Core Generation Logic --------------------

def build_character_pool(use_upper, use_digits, use_special):
    """
    Build the full pool of allowed characters, and keep track of
    each category separately so we can GUARANTEE at least one
    character from every selected category (a common security
    requirement - e.g. 'must contain a number').
    """
    pool = list(LOWERCASE)           # lowercase always included as the base
    required_chars = [secrets.choice(LOWERCASE)]

    if use_upper:
        pool += list(UPPERCASE)
        required_chars.append(secrets.choice(UPPERCASE))

    if use_digits:
        pool += list(DIGITS)
        required_chars.append(secrets.choice(DIGITS))

    if use_special:
        pool += list(SPECIAL)
        required_chars.append(secrets.choice(SPECIAL))

    return pool, required_chars


def generate_password(length, use_upper, use_digits, use_special):
    """
    Generate a secure random password.

    Uses the ACCUMULATOR PATTERN: we start with a small list of
    'required' characters (one per selected category) and keep
    appending securely-random characters until we hit the target
    length - exactly like total = total + new_expense, but here
    it's password_chars = password_chars + [new_char].
    """
    pool, password_chars = build_character_pool(use_upper, use_digits, use_special)

    # Fill the rest of the length with random picks from the full pool
    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    # Shuffle securely so the guaranteed characters aren't always at the front
    # (secrets has no shuffle, so we do a manual Fisher-Yates using secrets.randbelow)
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


# -------------------- Output / Feedback --------------------

def rate_strength(length, use_upper, use_digits, use_special):
    """Simple feedback so the user understands WHY a password is strong."""
    variety = 1 + use_upper + use_digits + use_special
    if length >= 16 and variety == 4:
        return " Very Strong"
    elif length >= 12 and variety >= 3:
        return " Strong"
    elif length >= 8:
        return " Moderate"
    else:
        return " Weak"


# -------------------- Main Program --------------------

def main():
    print("========= DECODELABS PASSWORD GENERATOR =========")
    print("Build a secure password using cryptographically safe randomness.\n")

    length = ask_length()
    use_upper = ask_yes_no("Include uppercase letters (A-Z)? (y/n): ")
    use_digits = ask_yes_no("Include numbers (0-9)? (y/n): ")
    use_special = ask_yes_no("Include special characters (@#$%&*!?)? (y/n): ")

    while True:
        password = generate_password(length, use_upper, use_digits, use_special)
        strength = rate_strength(length, use_upper, use_digits, use_special)

        print("\n---------------------------------")
        print(f" Generated Password: {password}")
        print(f" Strength: {strength}")
        print("---------------------------------\n")

        again = ask_yes_no("Generate another password with the same settings? (y/n): ")
        if not again:
            break

    print(" Stay secure! Never reuse passwords across sites.")


if __name__ == "__main__":
    main()
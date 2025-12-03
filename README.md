# PlayfairCipher-Python

---------------

> A complete and robust Python implementation of the Playfair Cipher, a classic symmetric encryption technique. This project demonstrates modular programming, algorithmic thinking, and professional testing using the `unittest` framework.

## 🚀 Overview

This repository contains the source code for a fully functional Playfair Cipher encryptor. The Playfair Cipher is a manual symmetric encryption technique that encrypts digraphs (pairs of letters) instead of single letters, making frequency analysis more difficult than with simple substitution ciphers.

The implementation is broken down into clear, testable components:
1.  **Grid Generation**: Creating the 5x5 cipher grid from a keyword.
2.  **Message Preparation**: Cleaning input, handling 'J' $\rightarrow$ 'I' substitution, separating double letters (e.g., 'LL' $\rightarrow$ 'LX'), and padding odd-length messages.
3.  **Encryption Logic**: Applying the three main Playfair rules (Same Row, Same Column, Rectangle) to transform digraphs.
4.  **Unit Testing**: Comprehensive tests using `unittest` to ensure all components function correctly under various edge-case scenarios.






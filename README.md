<h1>Tic Tac Toe Game</h1>
<p><strong>Version 1.0 – Turtle Edition</strong></p>

<p>
A graphical implementation of the classic Tic Tac Toe game built entirely using Python’s 
<code>turtle</code> module. This version includes a custom-drawn user interface, simple 
animations, game modes, and a persistent leaderboard system.
</p>

<h2>✨ Features</h2>
<ul>
    <li><strong>Custom UI Elements:</strong> All buttons, screens, and shapes are drawn manually using Turtle graphics.</li>
    <li><strong>AI Opponent:</strong> Single-player mode includes a basic smart AI that tries to win or block the player.</li>
    <li><strong>Leaderboard:</strong> Automatically saves wins, losses, and draws to <code>leaderboard.json</code>.</li>
    <li><strong>Dark Theme:</strong> Clean, minimal, dark-themed interface built with Turtle.</li>
    <li><strong>Basic Animations:</strong> Winning line animations and smooth transitions.</li>
</ul>

<h2>🛠️ Technical Overview</h2>
<p>This version is built as a single Python script <code>main.py</code> and uses:</p>
<ul>
    <li><strong>State Management:</strong> Controls turns, board state, and game modes (PvP / PvAI).</li>
    <li><strong>Rendering Engine:</strong> Multiple Turtle instances handle UI, board drawing, and animations.</li>
    <li><strong>Input Handling:</strong> Click-based interaction mapped to grid cells and menu buttons.</li>
</ul>

<h2>🚀 Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.x installed</li>
    <li>Only uses built-in modules: <code>turtle</code>, <code>time</code>, <code>random</code>, <code>json</code>, <code>os</code></li>
</ul>

<h3>Installation</h3>
<p>Clone the repository:</p>
<pre><code>git clone https://github.com/muthu17ks/Tic-Tac-Toe-Game.git
</code></pre>

<p>Navigate to the project folder:</p>
<pre><code>cd Tic-Tac-Toe-Game
</code></pre>

<h3>Run the Game</h3>
<p>Execute the script:</p>
<pre><code>python main.py
</code></pre>

<h2>🎮 How to Play</h2>
<ul>
    <li><strong>Main Menu:</strong> Choose 1-Player (AI), 2-Player, or view Leaderboard.</li>
    <li><strong>Gameplay:</strong> Click any empty cell to place X or O.</li>
    <li><strong>Goal:</strong> Make a straight line of 3 symbols horizontally, vertically, or diagonally.</li>
    <li><strong>Result:</strong> A result screen appears and stats are saved automatically.</li>
</ul>

<h2>📂 Project Structure</h2>
<pre><code>Tic-Tac-Toe-Game/
│
├── main.py                 # Main game source code
├── leaderboard.json        # Auto-generated statistics file
└── README.md               # Documentation
</code></pre>

<h2>📌 Future Versions</h2>
<p>
A new release (v2.0) is planned, featuring a complete rewrite using <strong>Tkinter</strong> 
for a more modern and responsive GUI.  
This version (v1.0) is the original Turtle-based implementation.
</p>

<h2>🤝 Contributing</h2>
<p>Contributions are welcome! Submit a Pull Request if you want to improve or add features.</p>

<h2>📄 License</h2>
<p>
Licensed under the MIT License. See <code>LICENSE</code> for details.
</p>

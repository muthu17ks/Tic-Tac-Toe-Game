<h1>Tic Tac Toe Game</h1>

<p>
A graphical implementation of the classic Tic Tac Toe game built in Python. 
This project uses the <code>turtle</code> module to create a custom interface, 
stores basic player statistics, and includes a simple dark-themed layout.
</p>

<h2>✨ Features</h2>
<ul>
    <li><strong>Custom UI Elements:</strong> Basic button system, rounded rectangles, and dialog-like screens created using Turtle graphics.</li>
    <li><strong>Smart AI:</strong> The single-player mode includes an AI that tries to win or block the opponent.</li>
    <li><strong>Leaderboard:</strong> Saves and loads lifetime statistics (Wins/Losses/Draws) using <code>leaderboard.json</code>.</li>
    <li><strong>Dark Theme:</strong> A clean, minimal dark-colored interface.</li>
    <li><strong>Simple Animations:</strong> Basic line-drawing animations for winning moves and transitions.</li>
</ul>

<h2>🛠️ Technical Overview</h2>
<p>The project is a single-file application <code>(main.py)</code> that includes:</p>
<ul>
    <li><strong>State Management:</strong> Handles turns, board updates, and game modes (PvP or PvAI).</li>
    <li><strong>Rendering:</strong> Uses multiple Turtle instances to draw UI, game board, and animations separately.</li>
    <li><strong>Input Handling:</strong> Maps mouse clicks to grid positions and menu buttons.</li>
</ul>

<h2>🚀 Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.x installed on your system.</li>
    <li>Uses only standard libraries: <code>turtle</code>, <code>random</code>, <code>time</code>, <code>json</code>, <code>os</code>.</li>
</ul>

<h3>Installation</h3>
<p>Clone the repository:</p>
<pre><code>git clone https://github.com/muthu17ks/Tic-Tac-Toe-Game.git
</code></pre>

<p>Navigate to the project directory:</p>
<pre><code>cd Tic-Tac-Toe-Game
</code></pre>

<h3>Running the Game</h3>
<p>Run the script using Python:</p>
<pre><code>python main.py
</code></pre>

<h2>🎮 How to Play</h2>
<ul>
    <li><strong>Main Menu:</strong> Select 1 Player (AI), 2 Players, or view the Leaderboard.</li>
    <li><strong>Gameplay:</strong> Click on an empty cell to place X or O.</li>
    <li><strong>Objective:</strong> Form a line of 3 marks horizontally, vertically, or diagonally.</li>
    <li><strong>Game Over:</strong> A result screen appears and your stats are saved automatically.</li>
</ul>

<h2>📂 Project Structure</h2>
<pre><code>Tic-Tac-Toe-Game/
│
├── main.py                 # Main game source code
├── leaderboard.json        # Automatically created (stores stats)
└── README.md               # Documentation
</code></pre>

<h2>🤝 Contributing</h2>
<p>Contributions are welcome! You can submit a Pull Request.</p>
<ol>
    <li>Fork the repository.</li>
    <li>Create a feature branch: <code>git checkout -b feature/NewFeature</code></li>
    <li>Commit your changes: <code>git commit -m "Add new feature"</code></li>
    <li>Push the branch: <code>git push origin feature/NewFeature</code></li>
    <li>Open a Pull Request.</li>
</ol>

<h2>📄 License</h2>
<p>
This project is licensed under the MIT License — see the <code>LICENSE</code> file for details.
</p>

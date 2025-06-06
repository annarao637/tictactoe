import streamlit as st
import random

# Page setup
st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #c2e9fb, #a1c4fd);
        }
        .stButton>button {
            font-size: 40px;
            height: 100px;
            width: 100px;
            margin: 5px;
            font-weight: bold;
            border-radius: 12px;
            transition: background-color 0.3s ease;
        }
        .mode-select {
            text-align: center;
            margin-top: 30px;
        }
        .highlight {
            background-color: #90ee90 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize or reset session state variables
def init_state():
    st.session_state.page = "home"
    st.session_state.mode = None
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.player1_name = "Player 1"
    st.session_state.player2_name = "Player 2"
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
    st.session_state.winning_combo = []
    st.session_state.score_updated = False

if "page" not in st.session_state:
    init_state()

# Game logic
def check_winner():
    b = st.session_state.board
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for combo in wins:
        i,j,k = combo
        if b[i] == b[j] == b[k] != "":
            st.session_state.winning_combo = combo
            return b[i]
    if "" not in b:
        return "Draw"
    return None

def make_move(index, player):
    if st.session_state.board[index] == "" and st.session_state.winner is None:
        st.session_state.board[index] = player
        st.session_state.winner = check_winner()
        st.session_state.score_updated = False  # reset flag on new move
        return True
    return False

def bot_move():
    empty = [i for i, v in enumerate(st.session_state.board) if v == ""]
    if empty and st.session_state.winner is None:
        move = random.choice(empty)
        make_move(move, "O")

def get_player_name(symbol):
    if st.session_state.mode == "single":
        return st.session_state.player1_name if symbol == "X" else "Bot"
    else:
        return st.session_state.player1_name if symbol == "X" else st.session_state.player2_name

# Update scoreboard only once per game end
def update_scoreboard():
    if not st.session_state.score_updated and st.session_state.winner:
        st.session_state.score[st.session_state.winner] += 1
        st.session_state.score_updated = True

if st.session_state.page == "home":
    st.title("🎮 Welcome to Tic Tac Toe")
    st.markdown("<div class='mode-select'>", unsafe_allow_html=True)
    st.subheader("Select Game Mode")

    mode = st.radio("Choose Game Mode:", ("Single Player", "Two Player"))

    if mode == "Two Player":
        p1 = st.text_input("Player 1 Name:", st.session_state.player1_name)
        p2 = st.text_input("Player 2 Name:", st.session_state.player2_name)
        if p1.strip() != "":
            st.session_state.player1_name = p1.strip()
        if p2.strip() != "":
            st.session_state.player2_name = p2.strip()
    else:
        p1 = st.text_input("Your Name:", st.session_state.player1_name)
        st.session_state.player1_name = p1.strip() if p1.strip() != "" else "Player 1"
        st.session_state.player2_name = "Bot"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Single Player") and mode == "Single Player":
            st.session_state.mode = "single"
            st.session_state.page = "game"
            st.session_state.board = [""] * 9
            st.session_state.current_player = "X"
            st.session_state.winner = None
            st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
            st.session_state.winning_combo = []
            st.session_state.score_updated = False
    with col2:
        if st.button("Start Two Player") and mode == "Two Player":
            st.session_state.mode = "two"
            st.session_state.page = "game"
            st.session_state.board = [""] * 9
            st.session_state.current_player = "X"
            st.session_state.winner = None
            st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
            st.session_state.winning_combo = []
            st.session_state.score_updated = False

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "game":
    st.title("🧩 Tic Tac Toe")

    # Show scoreboard
    update_scoreboard()
    st.markdown(f"""
    <h4>Scoreboard</h4>
    <p>{st.session_state.player1_name} (X): {st.session_state.score['X']} &nbsp;&nbsp;&nbsp;
    {st.session_state.player2_name} (O): {st.session_state.score['O']} &nbsp;&nbsp;&nbsp;
    Draws: {st.session_state.score['Draw']}</p>
    """, unsafe_allow_html=True)

    # Show current player's turn
    current_name = get_player_name(st.session_state.current_player)
    st.markdown(f"### 🕹️ {current_name}'s turn ({st.session_state.current_player})")

    cols = st.columns(3)

    for i in range(3):
        for j in range(3):
            idx = 3 * i + j
            display = st.session_state.board[idx]
            btn_label = display if display != "" else " "
            # Highlight winning combo
            style = ""
            if idx in st.session_state.winning_combo:
                style = "background-color: #90ee90;"
            # Color X and O differently with emojis (workaround)
            if display == "X":
                btn_label = f":blue[{display}]"
            elif display == "O":
                btn_label = f":red[{display}]"

            with cols[j]:
                if st.button(btn_label, key=idx):
                    if st.session_state.board[idx] == "" and st.session_state.winner is None:
                        if st.session_state.mode == "two":
                            if st.session_state.current_player == "X":
                                if make_move(idx, "X"):
                                    if st.session_state.winner is None:
                                        st.session_state.current_player = "O"
                            else:
                                if make_move(idx, "O"):
                                    if st.session_state.winner is None:
                                        st.session_state.current_player = "X"
                        else:
                            # Single player: player is X
                            if st.session_state.current_player == "X":
                                if make_move(idx, "X"):
                                    if st.session_state.winner is None:
                                        bot_move()

    # Show winner or draw messages
    if st.session_state.winner:
        if st.session_state.winner == "Draw":
            st.info("😐 It's a draw!")
        else:
            winner_name = get_player_name(st.session_state.winner)
            st.success(f"🏆 {winner_name} ({st.session_state.winner}) wins!")

    # Options
    st.markdown("### 🔁 Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Game"):
            st.session_state.board = [""] * 9
            st.session_state.current_player = "X"
            st.session_state.winner = None
            st.session_state.winning_combo = []
            st.session_state.score_updated = False

    with col2:
        if st.button("🏠 Back to Home"):
            init_state()

import re
import sys
import chess
import chess.uci
import chess.pgn
from pprint import pprint

game_commands = ['fen', 'legal', 'help', 'exit', 'dif', 'board','undo']


#here you need to add the path to stockfish or some other uci engine(that will probably work)
engine = chess.uci.popen_engine("./stockfish-9-64")
engine.uci()
print(engine.author)
san_regex = re.compile('([KQNBR]([a-h][1-8])?x)?[KQNBR]?[a-h][1-8]$|[0o]-[o0]$')
uci_regex = re.compile('[a-h][1-8][a-h][1-8]')

moves = []
board = chess.Board()
dif = 1

engine.position(board)


def execute_command(command):
	print('executing the command')
	if command == 'fen':
		print(board.fen())
	elif command == 'legal':
		legal = board.legal_moves
		print(legal)
	elif command == 'help':
		print('Welcome to Blind Chess, you can enter moves both in SAN form(e4, Kf6 etc.) or UCI (e2e4,e7e5).\n'+
		 	'Extra commands:\n'+
		 	'1. fen:   returns a FEN representation of the board\n' +
		 	'2. legal: returns all legal moves\n' +
		 	'3. undo:  unmakes last move\n' +
		 	'4. dif:   difficulty level(1-5)\n' +
		 	'5. help:  returns this menu\n' +
			'6. board: see the board\n' +
			'7. exit:  exit Blind Chess')
	elif command == 'undo':
		board.pop()
		board.pop()
		print('Undid last move!')
	elif command == 'board':
		print(board)
	elif command == 'dif':
		dif = input("Enter game difficulty(1-5):")
	elif command == 'exit':
		sys.exit("Goodbye!")



while board.is_checkmate() == False :
	players_move = input("Please enter your move:")

	try:
		if players_move in game_commands:
			execute_command(players_move)
			continue
		else:
			mymove = board.parse_san(players_move)
			moves.append(board.san(mymove))
			board.push(mymove)
	except Exception:
		print("Move or command not found, please try entering a valid move or command")
		continue

		if board.is_game_over():
			print('Game over')
			sys.exit("Goodbye!")

	if mymove != 0000 :
		engine.position(board)
		engine_move = engine.go(movetime=(dif*500))
		moves.append(board.san(engine_move.bestmove))
		board.push(engine_move.bestmove)

		#print all moves after each round
		index = 0
		move_num = 0
		for m in moves:
			if (index % 2) == 0 :
				move_num = move_num + 1
				print(str(move_num)+'.'+ m, end='')
			else :
				print(' ,'+m)

			index = index + 1

	if board.is_game_over():
		input('Game over')
		sys.exit("Goodbye!")

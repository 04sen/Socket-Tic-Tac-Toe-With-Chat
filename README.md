# Socket-Tic-Tac-Toe-With-Chat
As part of my continued assessment during my study at the University of the South Pacific. Dated: April, 2024.

## Chat and Tic Tac Toe Application

This project combines a chat application with a game of Tic Tac Toe, implementing a client-server architecture using Python sockets. Players can communicate via chat while playing Tic Tac Toe in a networked environment. The interface is built with CustomTkinter for a modern look.

## Features

- Real-time chat functionality during the game.
- Play Tic Tac Toe with another networked player.
- Interface designed with CustomTkinter for enhanced aesthetics.
- Client-server communication using sockets.
- Game options to play against another human or against the computer.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Access to a terminal or command-line interface

## Dependencies

To run this application, you'll need to install the following modules:

- `customtkinter`
- `socket`
- `threading`
- `random`
- `time`

You can install the required package using pip:

```bash
pip install customtkinter
```
## Installation 

To install the application, follow these steps:

1. **Clone the repository or download the source code:**

```bash
git clone https://github.com/04sen/CS310-2024.git
```
2. **Navigate to the project directory**

```bash
cd CS310-2024

(or any other method as per your system)
```

## Usage

To run the application, you need to start both the server and the client.

### Starting the Server

Open a terminal and execute the following command:
```bash
python server.py
```
### Starting the Client

Open another terminal and execute the following command:
```bash 
python client.py
```

Enter your username and select a game mode within the Graphical User Interface to start playing.

## Contributing

Contributions to the project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Make your changes.
4. Commit your changes (git commit -am 'Add some feature').
5. Push to the branch (git push origin feature/YourFeature).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

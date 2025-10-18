import React from 'react'

const WinModal = ({ show, message, onPlayAgain, onNewGame }) => {
  if (!show) return null

  return (
    <div className="win-modal active">
      <div className="win-modal-content">
        <div className="win-message">{message}</div>
        <button className="play-again-btn" onClick={onPlayAgain}>
          PLAY AGAIN
        </button>
        <button className="play-again-btn new-game-btn" onClick={onNewGame}>
          BACK TO MAIN
        </button>
      </div>
    </div>
  )
}

export default WinModal

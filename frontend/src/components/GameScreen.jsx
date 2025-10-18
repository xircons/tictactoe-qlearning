import React from 'react'

const GameScreen = ({ 
  show, 
  board, 
  scores, 
  playerNames, 
  onCellClick, 
  onResetGame, 
  onBackToMain 
}) => {
  if (!show) return null

  return (
    <div className="game-screen active">
      <div className="game-header">
        <div className="player-names">{playerNames.X} VS AI</div>
        <div className="score-board">
          <div className="score-item">
            <div className="score-label">{playerNames.X}</div>
            <div className="score-value">{scores.X}</div>
          </div>
          <div className="score-item">
            <div className="score-label">DRAWS</div>
            <div className="score-value">{scores.draw}</div>
          </div>
          <div className="score-item">
            <div className="score-label">{playerNames.O}</div>
            <div className="score-value">{scores.O}</div>
          </div>
        </div>
      </div>
      
      <div className="game-board">
        {board.map((cell, index) => (
          <div 
            key={index}
            className={`cell ${cell ? 'taken' : ''}`}
            onClick={() => onCellClick(index)}
            data-index={index}
          >
            {cell && (
              <span className={`cell-content ${cell.toLowerCase()}`}>
                {cell}
              </span>
            )}
          </div>
        ))}
      </div>
      
      <div className="game-status"></div>
      <button className="reset-btn" onClick={onResetGame}>
        RESET GAME
      </button>
      <button className="back-btn" onClick={onBackToMain}>
        BACK
      </button>
    </div>
  )
}

export default GameScreen

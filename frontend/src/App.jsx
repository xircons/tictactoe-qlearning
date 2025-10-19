import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Layout from './components/Layout'
import SlideMessage from './components/SlideMessage'
import AchievementNotification from './components/AchievementNotification'
import HomePage from './pages/HomePage'
import GamePage from './pages/GamePage'
import SettingsPage from './pages/SettingsPage'
import HistoryPage from './pages/HistoryPage'
import AboutPage from './pages/AboutPage'

function App() {
  const { showSlideMessage, slideMessage, animationSpeed } = useSelector((state) => state.settings)

  // Apply animation speed to body
  useEffect(() => {
    document.body.className = `animation-speed-${animationSpeed}`
  }, [animationSpeed])

  // Initialize debug logging and generate stars
  useEffect(() => {
    console.log('[GAME INIT] Tic-Tac-Toe with AI - Redux + Router Edition')
    console.log('==========================================')

    // Generate stars
    const starsContainer = document.getElementById('stars')
    if (starsContainer) {
      starsContainer.innerHTML = ''
      
      for (let i = 0; i < 80; i++) {
        const star = document.createElement('div')
        star.className = 'star'
        star.style.left = Math.random() * 100 + '%'
        star.style.top = Math.random() * 100 + '%'
        star.style.animationDelay = Math.random() * 3 + 's'
        starsContainer.appendChild(star)
      }
    }
  }, [])

  return (
    <>
      <div className="stars" id="stars"></div>
      <SlideMessage 
        message={slideMessage}
        show={showSlideMessage}
      />
      <AchievementNotification />
      
      <div className="phone-container pixel-corners">
        <div className="phone-notch pixel-corners">
          <div className="phone-speaker"></div>
        </div>
        <div className="phone-screen pixel-corners">
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/game" element={<GamePage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/about" element={<AboutPage />} />
            </Routes>
          </Layout>
        </div>
      </div>
    </>
  )
}

export default App

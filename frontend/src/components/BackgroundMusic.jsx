import React, { useEffect, useRef, useState } from 'react'
import { useSelector } from 'react-redux'

const BackgroundMusic = () => {
  const audioRef = useRef(null)
  const [isLoaded, setIsLoaded] = useState(false)
  const { musicEnabled, musicVolume } = useSelector((state) => state.settings)

  // Handle audio loading
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleLoadedData = () => {
      setIsLoaded(true)
      console.log('[MUSIC] Background music loaded successfully')
    }

    const handleError = (e) => {
      console.error('[MUSIC] Error loading background music:', e)
    }

    audio.addEventListener('loadeddata', handleLoadedData)
    audio.addEventListener('error', handleError)

    return () => {
      audio.removeEventListener('loadeddata', handleLoadedData)
      audio.removeEventListener('error', handleError)
    }
  }, [])

  // Handle music playback based on settings
  useEffect(() => {
    const audio = audioRef.current
    console.log('[MUSIC DEBUG] Music effect triggered - musicEnabled:', musicEnabled, 'isLoaded:', isLoaded, 'volume:', musicVolume)
    
    if (!audio || !isLoaded) {
      console.log('[MUSIC DEBUG] Music not ready - audio exists:', !!audio, 'isLoaded:', isLoaded)
      return
    }

    audio.volume = musicVolume / 100

    if (musicEnabled) {
      console.log('[MUSIC DEBUG] Attempting to play music...')
      audio.play().catch((error) => {
        console.warn('[MUSIC] Autoplay prevented by browser:', error)
        // Don't show error to user, just log it
      })
    } else {
      console.log('[MUSIC DEBUG] Music disabled, pausing...')
      audio.pause()
    }
  }, [musicEnabled, musicVolume, isLoaded])

  // Handle volume changes
  useEffect(() => {
    const audio = audioRef.current
    if (audio) {
      audio.volume = musicVolume / 100
    }
  }, [musicVolume])

  // Handle music end - loop the track
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleEnded = () => {
      if (musicEnabled) {
        audio.currentTime = 0
        audio.play().catch((error) => {
          console.warn('[MUSIC] Error restarting music:', error)
        })
      }
    }

    audio.addEventListener('ended', handleEnded)
    return () => audio.removeEventListener('ended', handleEnded)
  }, [musicEnabled])

  // Handle visibility change - pause when tab is not active
  useEffect(() => {
    const handleVisibilityChange = () => {
      const audio = audioRef.current
      if (!audio || !isLoaded) return

      if (document.hidden) {
        audio.pause()
      } else if (musicEnabled) {
        audio.play().catch((error) => {
          console.warn('[MUSIC] Error resuming music:', error)
        })
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange)
  }, [musicEnabled, isLoaded])

  return (
    <audio
      ref={audioRef}
      preload="auto"
      loop
      style={{ display: 'none' }}
    >
      <source src="./sounds/songs/Street Fighter II Arcade Music - Zangief Stage - CPS1 [TosG0dWQSXk].webm" type="audio/webm" />
      <source src="./sounds/songs/Street Fighter II Arcade Music - Zangief Stage - CPS1 [TosG0dWQSXk].webm" type="audio/mpeg" />
      Your browser does not support the audio element.
    </audio>
  )
}

export default BackgroundMusic

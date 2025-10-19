import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  theme: 'pixel', // 'pixel', 'modern', 'classic'
  soundEnabled: true,
  soundVolume: 50, // 0-100
  musicVolume: 25, // 0-100
  animationSpeed: 'normal', // 'slow', 'normal', 'fast'
  playerAvatar: 'default',
  showSlideMessage: false,
  slideMessage: '',
  lastDifficulty: 'hard', // Remember last selected difficulty
  lastGameMode: 'ai' // Remember last selected game mode
}

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    setTheme: (state, action) => {
      state.theme = action.payload
    },
    setSoundEnabled: (state, action) => {
      state.soundEnabled = action.payload
    },
    setAnimationSpeed: (state, action) => {
      state.animationSpeed = action.payload
    },
    setPlayerAvatar: (state, action) => {
      state.playerAvatar = action.payload
    },
    showSlideMessage: (state, action) => {
      state.showSlideMessage = true
      state.slideMessage = action.payload
    },
    hideSlideMessage: (state) => {
      state.showSlideMessage = false
    },
    toggleSound: (state) => {
      state.soundEnabled = !state.soundEnabled
    },
    setSoundVolume: (state, action) => {
      state.soundVolume = action.payload
    },
    setMusicVolume: (state, action) => {
      state.musicVolume = action.payload
    },
    setLastDifficulty: (state, action) => {
      state.lastDifficulty = action.payload
    },
    setLastGameMode: (state, action) => {
      state.lastGameMode = action.payload
    }
  }
})

export const {
  setTheme,
  setSoundEnabled,
  setAnimationSpeed,
  setPlayerAvatar,
  showSlideMessage,
  hideSlideMessage,
  toggleSound,
  setSoundVolume,
  setMusicVolume,
  setLastDifficulty,
  setLastGameMode
} = settingsSlice.actions

export default settingsSlice.reducer


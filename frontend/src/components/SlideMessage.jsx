import React from 'react'

const SlideMessage = ({ message, show }) => {
  return (
    <div className={`slide-message ${show ? 'show' : 'hide'}`}>
      {message}
    </div>
  )
}

export default SlideMessage

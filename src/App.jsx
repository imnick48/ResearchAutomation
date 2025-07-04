import { useState } from 'react'
import ResearchSec from './Components/ResearchSec'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ResearchSec />
    </>
  )
}

export default App

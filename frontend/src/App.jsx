import React from 'react'
import Header from './components/Header'
import Home from './pages/Home'

export default function App(){
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white text-gray-900">
      <Header />
      <main className="max-w-4xl mx-auto p-6">
        <Home />
      </main>
    </div>
  )
}

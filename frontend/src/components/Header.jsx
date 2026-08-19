import React from 'react'

export default function Header(){
  return (
    <header className="bg-white border-b">
      <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 text-white flex items-center justify-center font-bold rounded">SCAN</div>
          <div>
            <h1 className="text-lg font-semibold">ScanArmor</h1>
            <p className="text-xs text-gray-500">Security scanning for small business websites</p>
          </div>
        </div>
        <nav className="text-sm text-gray-600">
          <a className="mr-4 hover:underline" href="#">Docs</a>
          <a className="hover:underline" href="#">Help</a>
        </nav>
      </div>
    </header>
  )
}

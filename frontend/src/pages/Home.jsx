import React, { useState, useEffect } from 'react'

export default function Home() {
  const [url, setUrl] = useState('')
  const [scanId, setScanId] = useState(null)
  const [scanResult, setScanResult] = useState(null)
  const [loading, setLoading] = useState(false)

  // Submit new scan
  async function submit() {
    if (!url) return
    setLoading(true)
    setScanResult(null)
    
    try {
      const res = await fetch('http://localhost:8000/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await res.json()
      setScanId(data.scan_id)
    } catch (err) {
      console.error("Failed to submit scan:", err)
      setLoading(false)
    }
  }

  // Poll API to fetch scan results when scanId changes
  useEffect(() => {
    if (!scanId) return

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/scan/${scanId}`)
        const data = await res.json()

        if (data.status === 'completed') {
          setScanResult(data.results)
          setLoading(false)
          clearInterval(interval)
        }
      } catch (err) {
        console.error("Error fetching scan status:", err)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [scanId])

  // Download PDF Report trigger
  const downloadPDF = () => {
    if (scanId) {
      window.open(`http://localhost:8000/api/scan/${scanId}/pdf`, '_blank')
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold">Scan Armor</h1>
      <p className="text-gray-600">
        Scan your website for common security issues. Only scan sites you own or have permission to test.
      </p>

      <div className="mt-4">
        <input 
          className="border p-2 w-full rounded" 
          placeholder="https://example.com" 
          value={url} 
          onChange={e => setUrl(e.target.value)} 
        />
        <button 
          className="mt-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50" 
          onClick={submit}
          disabled={loading}
        >
          {loading ? 'Scanning...' : 'Scan Now'}
        </button>
      </div>

      {/* Display Scan Progress & ID */}
      {scanId && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          <p className="font-semibold text-gray-700">Scan ID: {scanId}</p>
          <p className="text-sm text-gray-500">Status: {scanResult ? 'Completed' : 'Processing...'}</p>
        </div>
      )}

      {/* Display Results & Export Button */}
      {scanResult && (
        <div className="mt-6 p-6 border rounded bg-white shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Scan Results</h2>
            {/* BUTTON EXPORT PDF */}
            <button 
              onClick={downloadPDF}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-semibold"
            >
              Export PDF Report
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4 p-4 bg-gray-100 rounded">
            <div>
              <span className="text-gray-500">Score:</span> 
              <span className="ml-2 font-bold text-lg">{scanResult.score} / 100</span>
            </div>
            <div>
              <span className="text-gray-500">Grade:</span> 
              <span className="ml-2 font-bold text-lg">{scanResult.grade}</span>
            </div>
          </div>

          <h3 className="font-semibold text-lg mb-2">Issues Found ({scanResult.issues?.length || 0})</h3>
          <ul className="space-y-2">
            {scanResult.issues?.map((issue, idx) => (
              <li key={idx} className="p-3 border rounded bg-gray-50">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-800">{issue.title}</span>
                  <span className="text-xs uppercase px-2 py-1 bg-gray-200 rounded font-bold">
                    {issue.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1">{issue.detail}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
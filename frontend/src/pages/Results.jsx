import React from 'react'

export default function Results({result}){
  if(!result) return <div className="p-6">No results</div>
  return (
    <div className="p-6">
      <h2 className="text-2xl">Results for {result.target}</h2>
      <p>Score: {result.score} ({result.grade})</p>
      <div className="mt-4">
        {result.issues.map((i,idx)=> (
          <div key={idx} className="border rounded p-3 mb-2">
            <div className="font-semibold">{i.title}</div>
            <div className="text-sm text-gray-700">{i.detail}</div>
            <div className="text-xs text-gray-500">Severity: {i.severity}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

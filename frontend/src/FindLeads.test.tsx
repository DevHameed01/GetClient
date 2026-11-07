import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import { FindLeads } from './FindLeads'

describe('FindLeads', () => {
  it('renders the search criteria and an honest empty results state', () => {
    const markup = renderToStaticMarkup(createElement(FindLeads))

    expect(markup).toContain('name="industry"')
    expect(markup).toContain('name="location"')
    expect(markup).toContain('name="companySize"')
    expect(markup).toContain('name="keywords"')
    expect(markup).toContain('>Search businesses</button>')
    expect(markup).toContain('id="lead-results-heading">Businesses</h3>')
    expect(markup).toContain('Your search results will appear here')
    expect(markup).toContain('Discovery is not connected yet')
    expect(markup).not.toContain('Example business')
  })
})

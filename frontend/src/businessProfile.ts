import { apiRequest } from './api'

export type BusinessProfileInput = {
  business_name: string
  description: string
  industry: string
  website: string
  location: string
  products_and_services: string
  target_market: string
  unique_value_proposition: string
  communication_style: string
}

export type BusinessProfile = BusinessProfileInput & {
  id: string
  created_at: string
  updated_at: string
}

export async function updateBusinessProfile(
  profile: BusinessProfileInput,
  organizationId: string,
): Promise<BusinessProfile> {
  const payload: BusinessProfileInput = {
    business_name: profile.business_name,
    description: profile.description,
    industry: profile.industry,
    website: profile.website,
    location: profile.location,
    products_and_services: profile.products_and_services,
    target_market: profile.target_market,
    unique_value_proposition: profile.unique_value_proposition,
    communication_style: profile.communication_style,
  }

  return apiRequest<BusinessProfile>(
    '/business-profile',
    { method: 'PUT', body: JSON.stringify(payload) },
    organizationId,
  )
}

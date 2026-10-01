import content from './content.json'

export const section = (name) => content.sections.find((s) => s.name === name) || {}
export const faq = content.faq
export const socialProof = content.social_proof

import Eyebrow from './Eyebrow'

export default function SectionHead({ eyebrow, headline, light = false }) {
  return (
    <div className="mb-10 max-w-3xl">
      <Eyebrow light={light}>{eyebrow}</Eyebrow>
      <h2 className={`text-3xl font-bold leading-tight sm:text-[34px] ${light ? 'text-white' : ''}`}>{headline}</h2>
    </div>
  )
}

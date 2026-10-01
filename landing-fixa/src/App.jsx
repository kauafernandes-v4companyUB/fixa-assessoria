import Header from './components/Header'
import Hero from './components/Hero'
import Problem from './components/Problem'
import Solution from './components/Solution'
import HowItWorks from './components/HowItWorks'
import Authority from './components/Authority'
import Deliverables from './components/Deliverables'
import SocialProof from './components/SocialProof'
import Faq from './components/Faq'
import FinalCta from './components/FinalCta'
import Footer from './components/Footer'
import WhatsappFloat from './components/WhatsappFloat'

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Problem />
        <Solution />
        <HowItWorks />
        <Authority />
        <Deliverables />
        <SocialProof />
        <Faq />
        <FinalCta />
      </main>
      <Footer />
      <WhatsappFloat />
    </>
  )
}

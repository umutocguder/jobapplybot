# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

from typing import Dict, Any, Optional, List
from .profile import CandidateProfile
from .matcher import ResumeMatcher

class ProposalGenerator:
    """
    Generates high-converting freelance proposals and tailored corporate cover letters.
    """

    def __init__(self, profile: Optional[CandidateProfile] = None):
        self.profile = profile or CandidateProfile.load()
        self.matcher = ResumeMatcher()

    def generate_freelance_proposal(
        self,
        job_title: str,
        job_description: str,
        client_name: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Creates a punchy, hook-driven proposal for Upwork, Freelancer, or Bionluk.
        """
        resume_text = self.profile.to_resume_text()
        match_analysis = self.matcher.calculate_match_score(resume_text, job_description)
        matched_keywords = match_analysis.get("matched_keywords", [])
        relevant_projects = self.profile.find_relevant_projects(matched_keywords, limit=2)

        client_salutation = f"Hi {client_name}," if client_name else ("Hi there," if language == "en" else "Merhaba,")

        project_mentions = []
        for p in relevant_projects:
            name = p.get("name", "")
            desc = p.get("description", "")
            tech = ", ".join(p.get("technologies", []))
            if language == "en":
                project_mentions.append(f"- **{name}**: {desc} (Built with: {tech})")
            else:
                project_mentions.append(f"- **{name}**: {desc} (Teknolojiler: {tech})")

        projects_block = "\n".join(project_mentions) if project_mentions else ""

        if language == "en":
            body = (
                f"{client_salutation}\n\n"
                f"I reviewed your requirements for **{job_title}**. Having shipped enterprise iOS apps "
                f"reaching millions of users (such as İşCep and HomeWhiz IoT) as well as modern full-stack web platforms, "
                f"I have direct experience solving exactly what you described.\n\n"
                f"### Relevant Experience & Production Work:\n"
                f"{projects_block}\n\n"
                f"### How I will approach your project:\n"
                f"1. **Architecture & Scope Audit:** Review specifications, confirm UX flows, and set up a clean, maintainable architecture.\n"
                f"2. **Iterative Milestones:** Deliver working builds on a daily/weekly cadence with automated tests and clear communication.\n"
                f"3. **Production Polish:** Zero memory leaks, smooth 60fps UI, solid error handling, and end-to-end deployment.\n\n"
                f"### Quick Questions for You:\n"
                f"- Are there existing APIs or backend designs ready, or do we start from scratch?\n"
                f"- What is your target timeline or deadline for the first playable/usable milestone?\n\n"
                f"I am available to start immediately and can jump on a brief 10-minute call to align on details.\n\n"
                f"Best regards,\n"
                f"{self.profile.full_name}\n"
                f"Portfolio: {self.profile.github_url} | {self.profile.linkedin_url}"
            )
        else:
            body = (
                f"{client_salutation}\n\n"
                f"**{job_title}** için paylaştığınız gereksinimleri detaylıca inceledim. Milyonlarca kullanıcıya "
                f"hizmet veren kurumsal mobil uygulamalardan (İşCep, HomeWhiz IoT) modern tam donanımlı web platformlarına "
                f"kadar canlıya aldığım projeler sayesinde, ihtiyacınız olan yapıyı hızla hayata geçirebilirim.\n\n"
                f"### Doğrudan İlgili Referans Projelerim:\n"
                f"{projects_block}\n\n"
                f"### Çalışma ve Teslimat Planım:\n"
                f"1. **Kapsam ve Mimari Netleştirme:** Gereksinimleri doğrulayıp temiz, modüler ve sürdürülebilir mimariyi kurmak.\n"
                f"2. **Aşamalı ve Şeffaf İlerleme:** Düzenli aralıklarla çalışan derlemeler (build) sunarak süreci şeffaf yönetmek.\n"
                f"3. **Üretim Kalitesi:** Yüksek performans, sıfır çökme garantisi, temiz kod ve testlerle teslimat.\n\n"
                f"### Projeye Dair Hızlı Sorularım:\n"
                f"- Hazır bir API veya tasarım (Figma/Adobe XD) mevcut mu, yoksa sıfırdan mı kurgulayacağız?\n"
                f"- İlk çalışan prototip veya canlıya çıkış için hedeflediğiniz bir takvim var mı?\n\n"
                f"Detayları konuşmak ve hemen başlamak için dilediğiniz zaman iletişime geçebilirsiniz.\n\n"
                f"İyi çalışmalar,\n"
                f"{self.profile.full_name}\n"
                f"Portfolyo: {self.profile.github_url} | {self.profile.linkedin_url}"
            )

        return {
            "job_title": job_title,
            "match_score": match_analysis.get("score", 0.0),
            "matched_keywords": matched_keywords,
            "missing_keywords": match_analysis.get("missing_keywords", []),
            "proposal_text": body,
            "language": language
        }

    def generate_cover_letter(
        self,
        company: str,
        position: str,
        job_description: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Creates a corporate cover letter tailored to full-time job openings (LinkedIn, Indeed).
        """
        resume_text = self.profile.to_resume_text()
        match_analysis = self.matcher.calculate_match_score(resume_text, job_description)
        matched = match_analysis.get("matched_keywords", [])
        top_skills = ", ".join(matched[:8]) if matched else "iOS, Swift, Full-Stack Architecture"

        if language == "en":
            letter = (
                f"Dear Hiring Team at {company},\n\n"
                f"I am writing to express my strong enthusiasm for the **{position}** opportunity. "
                f"With over 4 years of proven software engineering experience building scalable mobile and full-stack "
                f"ecosystems, I have contributed directly to flagship platforms like İşCep, HomeWhiz, and DOA.\n\n"
                f"Your position strongly aligns with my core technical expertise, specifically around {top_skills}. "
                f"Throughout my career, I have prioritized writing clean, test-driven, and resilient software while "
                f"collaborating cross-functionally in high-velocity Agile teams.\n\n"
                f"Key value I bring to {company}:\n"
                f"- **Proven Enterprise Scale:** Shipped code trusted by millions of users daily with 99.9% crash-free sessions.\n"
                f"- **Deep Technical Versatility:** Expertise spanning native Swift/SwiftUI, Kotlin, Next.js, and Python.\n"
                f"- **Ownership Mindset:** Driving features from architectural discovery to production release and post-launch telemetry.\n\n"
                f"I would welcome the opportunity to discuss how my technical background and problem-solving drive can help "
                f"{company} achieve its engineering goals.\n\n"
                f"Sincerely,\n"
                f"{self.profile.full_name}\n"
                f"Email: {self.profile.email} | Phone: {self.profile.phone}\n"
                f"Resume: {self.profile.resume_url} | GitHub: {self.profile.github_url}"
            )
        else:
            letter = (
                f"{company} İnsan Kaynakları ve İşe Alım Ekibine,\n\n"
                f"{company} bünyesindeki **{position}** pozisyonuna olan yoğun ilgimi belirtmek isterim. "
                f"Milyonlarca kullanıcıya ulaşan yüksek ölçekli mobil ve tam donanımlı sistemler (İşCep, HomeWhiz, DOA) "
                f"üzerinde 4 yılı aşkın yazılım geliştirme deneyimine sahibim.\n\n"
                f"Aradığınız gereksinimler, özellikle {top_skills} konularındaki derin teknik birikimimle birebir örtüşmektedir. "
                f"Geliştirme süreçlerimde her zaman test güdümlü, temiz ve modüler mimarileri önceliklendirerek Agile "
                f"takımlarda yüksek katma değer ürettim.\n\n"
                f"{company} ekibine katabileceğim temel değerler:\n"
                f"- **Büyük Ölçekli Başarı Kanıtı:** Günlük milyonlarca aktif işlem gören, %99.9 çökmesiz çalışan sistemler.\n"
                f"- **Geniş Teknik Spektrum:** Native iOS (Swift/SwiftUI), Android (Kotlin), Next.js ve Python yetkinliği.\n"
                f"- **Uçtan Uca Sorumluluk:** Analiz ve mimari tasarımdan, canlıya çıkış ve telemetri takibine kadar eksiksiz sahiplenme.\n\n"
                f"Deneyimlerimi ve {company} hedeflerine nasıl katkı sağlayabileceğimi detaylandırmak üzere sizinle görüşmeyi çok isterim.\n\n"
                f"Saygılarımla,\n"
                f"{self.profile.full_name}\n"
                f"E-posta: {self.profile.email} | Telefon: {self.profile.phone}\n"
                f"CV: {self.profile.resume_url} | GitHub: {self.profile.github_url}"
            )

        return {
            "company": company,
            "position": position,
            "match_score": match_analysis.get("score", 0.0),
            "matched_keywords": matched,
            "cover_letter_text": letter,
            "language": language
        }

import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private supportedLanguages = ['en', 'pl']
  private defaultLanguage = 'en'
  private currentLanguage = ''

  constructor(public translate: TranslateService) {
    this.initializeLanguage();
  }

  private initializeLanguage(): void {
    this.translate.addLangs(this.supportedLanguages)
    this.translate.setDefaultLang(this.defaultLanguage)

    const browserLang = this.translate.getBrowserLang()
    const langToUse = browserLang?.match(/en|pl/) ? browserLang : this.defaultLanguage

    this.translate.use(langToUse)
    this.currentLanguage = langToUse
  }

  changeLanguage(lang: string): void {
    if (this.supportedLanguages.includes(lang)) {
      this.translate.use(lang);
      this.currentLanguage = lang
    }
  }

  getLanguages(): string[] {
    return this.supportedLanguages;
  }
  getCurrentLanguage(): string {
    return this.currentLanguage
  }
}

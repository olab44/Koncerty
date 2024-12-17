import { Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';

import { TranslationService } from '../services/translation/translation.service';

@Component({
  selector: 'app-top-bar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './top-bar.component.html',
  styleUrl: './top-bar.component.css'
})
export class TopBarComponent {
  @Input() isReturnAvailable: boolean = false;
  @Input() groupName: string = "";

  languages: string[]
  currentLanguage: string

  constructor(private translationService: TranslationService) {
    this.languages = this.translationService.getLanguages()
    this.currentLanguage = this.translationService.getCurrentLanguage()
  }

  changeLanguage(e: Event) {
    const target = e.target as HTMLSelectElement;
    const selectedLanguage = target.value;
    this.translationService.changeLanguage(selectedLanguage);
  }
}

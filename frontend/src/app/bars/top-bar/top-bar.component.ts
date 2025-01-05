import { Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';

import { TranslationService } from '../../services/translation/translation.service';
import { AuthService } from '../../services/authorization/auth.service';
import { SessionStateServiceService } from '../../services/session-state/session-state-service.service';

@Component({
  selector: 'app-top-bar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './top-bar.component.html',
  styleUrl: './top-bar.component.css'
})
export class TopBarComponent {
  @Input() isLogoutAvailable: boolean = true;
  @Input() isReturnAvailable: boolean = false;
  @Input() groupName: string = "";

  languages: string[]
  currentLanguage: string

  constructor(private translationService: TranslationService, private auth: AuthService, private state: SessionStateServiceService) {
    this.languages = this.translationService.getLanguages()
    this.currentLanguage = this.translationService.getCurrentLanguage()
  }

  changeLanguage(e: Event) {
    const target = e.target as HTMLSelectElement;
    const selectedLanguage = target.value;
    this.translationService.changeLanguage(selectedLanguage);
  }

  logOut() {
  const confirmLogout = window.confirm('Log out?');
  if (confirmLogout) {
    this.auth.clearToken();
    this.state.clearStorage();
    window.location.reload();
    }
  }
}

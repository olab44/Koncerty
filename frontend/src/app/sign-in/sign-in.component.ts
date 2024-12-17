import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {TranslateModule} from "@ngx-translate/core";

import { TopBarComponent } from '../bars/top-bar.component';
import { AuthService } from '../services/authorization/auth.service';

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [ TranslateModule, TopBarComponent ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent {
  constructor(
    private router: Router,
    public auth: AuthService,
  ) {}

  userSignIn() {
    // redirect to google
    // mock set token and goto home page
    this.auth.setToken('SUPERsecretSECRET_SSS')
    this.router.navigate(['/home'])
  }
}

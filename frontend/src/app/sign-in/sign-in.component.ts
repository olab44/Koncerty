import { Component } from '@angular/core';
import { TopBarComponent } from '../bars/top-bar.component';
import { AuthService } from '../authorization/auth.service';

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [ TopBarComponent ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent {
  constructor(
    public auth: AuthService
  ) {}

  userSignIn() {
    // redirect to googl
    // set token
    this.auth.setToken('SUPERsecretSECRET_SSS')
  }
}

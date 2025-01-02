import { Component, OnInit, NgZone } from '@angular/core';
import { TranslateModule } from "@ngx-translate/core";
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar.component';
import { AuthService } from '../services/authorization/auth.service';
import { BackendService } from '../services/backend-connection/backend.service';

declare const google: any;

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [ TranslateModule, TopBarComponent ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent implements OnInit {
  constructor(
    private backend: BackendService,
    private router: Router,
    public auth: AuthService,
    private ngZone: NgZone
  ) {}

  ngOnInit(): void {
    // Initialize the Google Sign-In Client
    google.accounts.id.initialize({
      client_id:"67926087995-g4ub7nr9u0mqooermb5hvhd1794pvvfq.apps.googleusercontent.com",
      context: "signin",
      ux_mode: "popup",
      callback: (response: any) => this.handleCredentialsResponse(response),
    })

    google.accounts.id.renderButton(
      document.getElementById('sign-in-icon'),
      { type: 'icon', size: 'large', theme: 'filled_black' }
    )
  }

  handleCredentialsResponse(response: any): void {
    this.backend.postToken(response.credential).subscribe({
      next: (response) => {
        console.log('Signed up successfully:', response);
        // what next? navigate to the next page? save token to use for identification later?
        this.auth.setToken("MOCKTOKEN")
        this.ngZone.run(() => { this.router.navigate(['/home']) });
      },
      error: (error) => {
        console.error('Error during signup:', error);
      },
    });
  }
}

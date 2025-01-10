import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';
import { CanActivateFn } from '@angular/router';
import { map, Observable } from 'rxjs';
import { SessionStateService } from '../session-state/session-state.service';

export const authGuard: CanActivateFn = (route, state): Observable<boolean> => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const sessionState = inject(SessionStateService)

  return sessionState.currentGroup.pipe(
    map(group => {
      if (!authService.isLoggedIn()) {
        router.navigate(['/']);
        return false;
      }

      const requiredRole = route.data?.['role'];
      if (requiredRole && group?.role !== requiredRole) {
        router.navigate(['/group'])
        return false
      }

      return true
    })
  );
};

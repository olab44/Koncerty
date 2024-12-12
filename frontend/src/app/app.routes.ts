import { Routes } from '@angular/router'

import { SignInComponent } from './sign-in/sign-in.component'
import { HomePageComponent } from './home-page/home-page.component'
import { GroupHubComponent } from './group-hub/group-hub.component'
import { MessageForumComponent } from './message-forum/message-forum.component'
import { EventCalendarComponent } from './event-calendar/event-calendar.component'
import { MusicCatalogueComponent } from './music-catalogue/music-catalogue.component'
import { EventDetailsComponent } from './event-details/event-details.component'
import { GroupControlComponent } from './group-control/group-control.component'

import { authGuard } from './authorization/auth.guard';

export const routes: Routes = [
    { path: 'home', component: HomePageComponent, canActivate: [authGuard] },
    { path: 'group/:group-name', component: GroupHubComponent, canActivate: [authGuard] },
    { path: 'group/:group-name/catalogue', component: MusicCatalogueComponent, canActivate: [authGuard] },
    { path: 'group/:group-name/calendar', component: EventCalendarComponent, canActivate: [authGuard] },
    { path: 'group/:group-name/event/:event-name', component: EventDetailsComponent, canActivate: [authGuard] },
    { path: 'group/:group-name/forum', component: MessageForumComponent, canActivate: [authGuard] },
    { path: 'group/:group-name/control', component: GroupControlComponent, canActivate: [authGuard] },
    { path: '', component: SignInComponent },
    { path: '**', redirectTo: 'home' }
]

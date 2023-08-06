README
######

Welcome to MBX, a mailbox scanner.

MBX can be used to scan a unix mailbox and make it searchable.

MBX is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

MBX can be found on pypi, see http://pypi.org/project/mbx

installation is through pypi::

 $ sudo pip3 install mbx --upgrade --force-reinstall

USAGE
=====

examples::

 $ mbx cmd
 cmd,find,scan,ver

 $ mbx scan ~/Desktop/25-1-2013
 reading from /home/bart/Desktop/25-1-2013
 ok 6892
 
 $ mbx find From==pvp- Subject -t
 0 Subject=RE: afspraak donderdag 11y41d
 1 Subject=RE: FW: verzoek afspraak gesprek 11y90d
 2 Subject=RE: afspraak Pjotr K en Henk O 11y85d
 3 Subject=RE: afspraak donderdag 11y42d
 4 Subject=RE: goede morgen 11y85d
 5 Subject=FW: verzoek afspraak gesprek 11y90d
 6 Subject=RE: Annemiek en afspraak Henk O 11y88d
 7 Subject=RE: afspraak donderdag 11y41d
 8 Subject=brief 11y215d
 9 Subject=RE: De gevaren van de FACT methodiek 8y232d
 10 Subject=Automatisch antwoord: Weer vergiftiging opgelopen bij de GGZ 9y103d
 11 Subject=RE: Weer vergiftiging opgelopen bij de GGZ 9y101d
 12 Subject=RE: Hulp 9y192d
 13 Subject=Automatisch antwoord: Brief aan de GGZ-NHN 8y228d
 14 Subject=Re: Klacht over het negeren van een signaal en het niet opbouwen van vertrouwen bij de client 9y1d

 $ mbx ver
 MBX 1

CONTACT
=======

| Bart Thate (bthate67@gmail.com)
| botfather on #dunkbots irc.freenode.net

'''
Created on 12 Apr 2017

@author: mozat
'''
import addressbook_pb2 as ad

addbook = ad.AddressBook()
person = addbook.person.add()
phone1 = person.phone.add()
phone1.number = "90082418"
phone1.type = ad.Person.MOBILE
phone2 = person.phone.add()
phone2.number = "90082418"
phone2.type = ad.Person.HOME
print len(person.phone)
print person.phone
print addbook

